import { NextResponse } from 'next/server'
import { retrieveToBuffer } from '@/lib/ftp'

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const arquivo = searchParams.get('arquivo')
  if (!arquivo) return new NextResponse('Caminho do arquivo não informado.', { status: 400 })
  try {
    const buf = await retrieveToBuffer(arquivo)
    const name = arquivo.split('/').filter(Boolean).pop() || 'arquivo'
    const isPdf = name.toLowerCase().endsWith('.pdf')
    const res = new NextResponse(buf, { headers: { 'Content-Type': isPdf ? 'application/pdf' : 'application/octet-stream' } })
    res.headers.set('Content-Disposition', `${isPdf ? 'inline' : 'attachment'}; filename="${name}"`)
    return res
  } catch (e: any) {
    return new NextResponse(String(e), { status: 500 })
  }
}
