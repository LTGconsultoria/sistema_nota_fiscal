import { NextResponse } from 'next/server'
import { retrieveToBuffer } from '@/lib/ftp'
import { pdfToImages, ocrImageToText, analyzeText } from '@/lib/ocr'

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const arquivo = searchParams.get('arquivo')
  if (!arquivo) return new NextResponse('Caminho do arquivo não informado.', { status: 400 })
  try {
    const buf = await retrieveToBuffer(arquivo)
    const imgs = pdfToImages(buf)
    let texto = ''
    for (const img of imgs) texto += ocrImageToText(img)
    const status = texto.includes('Nota Fiscal') ? 'OK' : 'Suspeito'
    const dados = analyzeText(texto)
    return NextResponse.json({ arquivo, status_previsto: status, texto: texto.slice(0, 3000), dados })
  } catch (e: any) {
    return new NextResponse(`Erro ao processar PDF com OCR: ${String(e)}`, { status: 500 })
  }
}
