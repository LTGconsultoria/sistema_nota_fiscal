import Link from 'next/link'

export default function Page() {
    return (
        <div style={{ padding: 24 }}>
            <h1>Sistema NFE (Next.js)</h1>
            <div style={{ marginTop: 16 }}>
                <Link href="/ftp">Abrir Explorador FTP</Link>
            </div>
        </div>
    )
}
