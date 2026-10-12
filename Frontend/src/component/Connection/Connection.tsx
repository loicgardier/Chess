import { useAtom, useAtomValue } from "jotai";
import { useState, type MouseEvent } from "react"
import { mainAtom, tokenAtom, urlAtom } from "../../atoms/atoms";
function Connection ( ){
    const [pseudo,setPseudo] = useState('')
    const [password,setPassword] = useState('')
    const url = useAtomValue(urlAtom)


    const [_,setToken] = useAtom(tokenAtom)
    const [__,setMain] =useAtom(mainAtom)

    const HandleSubmit = (event:MouseEvent)=>{
        event.preventDefault()
        fetch(url+"/users/connection",{
            method:'POST',
            headers:{
                'Content-Type': 'application/json',
                'accept': '*/*'
            },
            body:JSON.stringify({
                "pseudo_or_mail": pseudo,
                "password": password
            }),
            credentials: 'include',
        }).then(response=>{
            if(!response.ok)
                throw response
            return response.json()
        }).then(data=>{
            console.log(data)
            setToken(data.token)
            setMain('Accueil')

        })
    }

    return<>
    <h1>Connection</h1>
    <form>
        <input name="pseudo" placeholder="pseudo" type="text" onChange={e=>setPseudo(e.target.value)}></input>
        <input name="password" placeholder="password" type="password" onChange={e=>setPassword(e.target.value)}></input>
        <button onClick={e=>HandleSubmit(e)}>OK</button>
    </form>
    </>
}

export default Connection