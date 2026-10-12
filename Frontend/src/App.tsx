import './App.css'
import Header from './component/Header/Header'
import Connection from './component/Connection/Connection';
import { useEffect } from 'react';
import { useAtomValue,useAtom } from 'jotai';
import { urlAtom,mainAtom,tokenAtom } from './atoms/atoms';
import Inscription from './component/Inscription/Inscription';

function App() {

  const [main,_] = useAtom(mainAtom)
  const [__,setToken] = useAtom(tokenAtom)
  const url = useAtomValue(urlAtom)

  useEffect(()=>{
    fetch(url+"/users/refresh",{
            method:'POST',
            headers:{
                'accept': '*/*'
            },            
            credentials: 'include',
        }).then(response=>{
            if(!response.ok)
                throw response
            return response.json()
        }).then(data=>{
            console.log(data)
            setToken(data.token)
        }).catch(e=>{
          console.log(e)
        })
  },[])

  return (
    <>
      <Header/>
      {(()=>{
        switch(main){
          case 'Accueil': break;
          case 'Tournois' :break
          case 'Rondes' : break
          case 'Connection': return <Connection/>
          case 'Inscription': return <Inscription/>
        }
        return <></>
      })()}
    </>
  )
}

export default App
