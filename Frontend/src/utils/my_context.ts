import { createContext } from 'react'
import { type MyContextType } from '../types/my_context_type';
export  const MyContext = createContext<MyContextType|null>(null);