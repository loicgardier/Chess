import './App.css'
import Header from './component/Header/Header'
import { MyContext } from './utils/my_context';
import Connection from './component/Connection/Connection';
import { useEffect, useState } from 'react';

function App() {
  const Token = useState('')
  const Main = useState('Accueil')
  const context = {Token,Main}
  const [main,_] =context.Main

  useEffect(()=>{
    fetch("http://localhost:8000"+"/users/refresh",{
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
            Token[1](data.token)
        }).catch(e=>{
          console.log(e)
        })
  },[])

  return (
    <>
    <MyContext value={context}>
      <Header/>
      {(()=>{
        switch(main){
          case 'Accueil': break;
          case 'Connection': return <Connection/>
        }
        return <></>
      })()}
    </MyContext>

    </>
  )
}

export default App
