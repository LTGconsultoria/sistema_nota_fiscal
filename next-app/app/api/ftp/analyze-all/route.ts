import { NextResponse } from 'next/server'
import { connect, retrieveToBuffer } from '@/lib/ftp'
import { pdfToImages, ocrImageToText, analyzeText } from '@/lib/ocr'
import path from 'node:path'
import io from 'node:stream'

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  let dir = (searchParams.get('path') || '/').trim()
  if (!dir.endsWith('/')) dir += '/'
  try {
    const client = await connect()
    try {
      await client.cd(dir)
      const list = await client.list()
      const arquivos = list.filter(e => !e.isDirectory && e.name.toLowerCase().endsWith('.pdf')).map(e => e.name)
      let txt = ''
      for (const nome of arquivos) {
        const tmpRemote = path.posix.join(dir, nome)
        try {
          const buffer = await retrieveToBuffer(tmpRemote)
          const imgs = pdfToImages(buffer)
          let texto = ''
          for (const img of imgs) texto += ocrImageToText(img)
          const status = texto.includes('Nota Fiscal') ? 'OK' : 'Suspeito'
          const dados = analyzeText(texto)
          txt += `arquivo=${nome} | status=${status} | cnpj=${dados.cnpj || ''} | data=${dados.data_emissao || ''} | valor=${dados.valor_total || ''} | chave=${dados.chave_acesso || ''}\n`
        } catch (e: any) {
          txt += `arquivo=${nome} | erro=${String(e)}\n`
        }
      }
      const nome = dir.replace(/^\/+|\/+$/g, '').replace(/\/+/g, '_') || 'raiz'
      const res = new NextResponse(txt, { headers: { 'Content-Type': 'text/plain' } })
      res.headers.set('Content-Disposition', `attachment; filename="analise_${nome}.txt"`)
      return res
    } finally {
      client.close()
    }
  } catch (e: any) {
    return new NextResponse(`Erro ao processar pasta: ${String(e)}`, { status: 500 })
  }
}
