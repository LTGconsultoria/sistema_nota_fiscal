import Link from 'next/link'
import { cookies } from 'next/headers'

async function fetchList(path: string) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL || ''}/api/ftp/list?path=${encodeURIComponent(path)}`, { cache: 'no-store' })
  return res.json()
}

export default async function Page({ searchParams }: { searchParams: { path?: string } }) {
  const currentPath = (searchParams?.path || '/').replace(/\s+/g, ' ')
  const data = await fetchList(currentPath)
  const tmp = currentPath.endsWith('/') ? currentPath.slice(0, -1) : currentPath
  const idx = tmp.lastIndexOf('/')
  const parentPath = idx > 0 ? tmp.slice(0, idx + 1) : '/'
  return (
    <div style={{ padding: 24 }}>
      <h2>Explorador de Arquivos FTP</h2>
      <p><strong>Caminho Atual:</strong> {currentPath}</p>
      <div style={{ display: 'flex', gap: 8 }}>
        <button onClick={() => history.back()}>Voltar</button>
        <button onClick={() => history.forward()}>Avançar</button>
        <Link href={`/ftp?path=${encodeURIComponent(parentPath)}`}>Subir nível</Link>
        <a href={`/api/ftp/analyze-all?path=${encodeURIComponent(currentPath)}`}>Analisar IA (todos) e gerar TXT</a>
      </div>
      <h3 style={{ marginTop: 16 }}>Pastas</h3>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 16 }}>
        {data.directories?.length ? data.directories.map((d: string) => (
          <div key={d}>
            <Link href={`/ftp?path=${encodeURIComponent(currentPath)}${encodeURIComponent(d)}/`}>{d}</Link>
          </div>
        )) : <span>Sem pastas encontradas.</span>}
      </div>
      <h3 style={{ marginTop: 16 }}>Arquivos</h3>
      <table>
        <thead>
          <tr><th>Nome</th><th>Data</th><th>Ação</th></tr>
        </thead>
        <tbody>
          {data.files?.length ? data.files.map((f: any) => (
            <tr key={f.name}>
              <td>{f.name}</td>
              <td>{f.modified}</td>
              <td>
                <a href={`/api/ftp/get?arquivo=${encodeURIComponent(currentPath + f.name)}`} target="_blank">Visualizar</a>
                {' '}
                <a href={`/api/ftp/analyze?arquivo=${encodeURIComponent(currentPath + f.name)}`}>Analisar IA</a>
              </td>
            </tr>
          )) : (
            <tr><td colSpan={3}>Sem arquivos encontrados.</td></tr>
          )}
        </tbody>
      </table>
    </div>
  )
}
