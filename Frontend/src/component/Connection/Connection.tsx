import { use, useState, type MouseEvent } from "react"
import { MyContext } from "../../utils/my_context"
function Connection ( ){
    const [pseudo,setPseudo] = useState('')
    const [password,setPassword] = useState('')
    const context= use(MyContext)
    if(!context)
    {
        throw new Error('Missing context');
    }
    const [_,setToken] = context.Token 

    const HandleSubmit = (event:MouseEvent)=>{
        event.preventDefault()
        fetch("http://localhost:8000"+"/users/connection",{
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
                throw response.status
            return response.json()
        }).then(data=>{
            console.log(data)
            setToken(data.token)
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