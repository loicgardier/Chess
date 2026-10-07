import {  useState } from 'react'
import './App.css'
import Header from './component/Header'
import { TokenContext } from './utils/token_context';
function App() {
  const tokenUseState = useState('');
  return (
    <>
    <TokenContext value={tokenUseState}>
      <Header/>
    </TokenContext>

    </>
  )
}

export default App
