const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

async function request(path) {
  const response = await fetch(`${API_BASE_URL}${path}`)

  let body = null
  try {
    body = await response.json()
  } catch {
    body = null
  }

  if (!response.ok) {
    const detail = body?.detail || `Request failed with status ${response.status}`
    throw new Error(detail)
  }

  return body
}

export async function fetchSummoner(summonerName, tag) {
  return request(`/api/v1/summoner/${encodeURIComponent(summonerName)}/${encodeURIComponent(tag)}`)
}

export async function fetchMatchHistory(puuid, count = 5) {
  return request(`/api/v1/match-history/${encodeURIComponent(puuid)}?start=0&count=${count}`)
}

export async function fetchMatchCards(puuid, count = 5, forceRefresh = false) {
  return request(
    `/api/v1/match-cards/${encodeURIComponent(puuid)}?count=${count}&force_refresh=${forceRefresh}`,
  )
}
