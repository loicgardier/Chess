import { useAtom, useAtomValue } from "jotai";
import { useState, type MouseEvent } from "react"
import { mainAtom, tokenAtom, urlAtom } from "../../atoms/atoms";


function Inscription ( ){
    const [pseudo,setPseudo] = useState('')
    const [mail,setMail] = useState('')
    const [password,setPassword] = useState('')
    const [genre,setGenre] = useState('homme')
    const [elo,setElo] = useState(1200)
    const [birthdate,setBirthdate] = useState('')
    const [authorizemail,setAuthorizemail] = useState(true)
    const url = useAtomValue(urlAtom)


    const [_,setToken] = useAtom(tokenAtom)
    const [__,setMain] =useAtom(mainAtom)

    const HandleSubmit = (event:MouseEvent)=>{
        event.preventDefault()
        fetch(url+"/users/inscription",{
            method:'POST',
            headers:{
                'Content-Type': 'application/json',
                'accept': '*/*'
            },
            body:JSON.stringify({
                "pseudo": pseudo,
                "email": mail,
                "password": password,
                "genre": genre,
                "elo": elo,
                "date_de_naissance": birthdate,
                "allow_mail": authorizemail
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
    <h1>Inscription</h1>
    <form>
        <input name="pseudo" placeholder="Pseudo" type="text" onChange={e=>setPseudo(e.target.value)}></input>
        <input name="mail" placeholder="Mail" type="email" onChange={e=>setMail(e.target.value)}></input>
        <input name="password" placeholder="Password" type="password" onChange={e=>setPassword(e.target.value)}></input>
        <select name="genre" value={genre} onChange={e=>setGenre(e.target.value)}>
            <option value='homme'>Homme</option>
            <option value='femme'>Femme</option>
            <option value='autre'>Autre</option>
        </select>
        <input name="elo" placeholder="Elo" type="number" onChange={e=>setElo(parseInt(e.target.value))} defaultValue={1200}></input>
        <input name="birthdate" placeholder="Date de naissance" type="date" onChange={e=>setBirthdate(e.target.value)}></input>
        <label htmlFor="authorizemail">Authorisation d'envoi de mail:</label>
        <input name="authorizemail" placeholder="Authorisation d'envoi de mail" type="checkbox" onChange={e=>setAuthorizemail(e.target.checked)} defaultChecked={true}></input>
        <button onClick={e=>HandleSubmit(e)}>OK</button>
    </form>
    </>
}

export default Inscription