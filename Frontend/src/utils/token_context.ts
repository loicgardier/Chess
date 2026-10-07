import { createContext } from 'react'

export  const TokenContext = createContext<[string, React.Dispatch<React.SetStateAction<string>>]|null>(null);