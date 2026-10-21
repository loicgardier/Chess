export interface TournamentDetailType {
  id: number
  nom: string
  lieu: string
  inscript: number
  elo_min: number
  elo_max: number
  categories: any[]
  status: string
  ronde: number
  women_only: boolean
  date_de_fin_inscription: string
  can_register: boolean
  is_registered: boolean
  inscripts: string[]
  rencontres: Rencontre[]
}

export interface Rencontre {
  id: number
  blanc: string
  noir: string
  result: string
}
