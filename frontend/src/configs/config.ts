type Config = {
  apiUrl: string
}

const CONFIG: Config = {
  apiUrl: 'https://api.nomos.galicea.pl/',
}

if (typeof window !== "undefined")
  if (
    window.location.href.startsWith('http://localhost') ||
    window.location.href.startsWith('http://127.0.0.1')
  ) {
    alert('Dev. (adres lokalny)')
    CONFIG.apiUrl = 'http://localhost:8086/';
  }

export default CONFIG
