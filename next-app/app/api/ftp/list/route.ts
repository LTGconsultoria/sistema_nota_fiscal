import { NextResponse } from 'next/server'
import { listDir } from '@/lib/ftp'

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const path = searchParams.get('path') || '/'
  try {
    const { directories, files } = await listDir(path)
    return NextResponse.json({ currentPath: path, directories, files })
  } catch (e: any) {
    return NextResponse.json({ error: String(e) }, { status: 500 })
  }
}
