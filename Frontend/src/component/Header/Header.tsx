import './Header.css'
import { jwtDecode } from 'jwt-decode'
import type { MyJwt } from '../../@types/my_jwt'
import { type MouseEvent } from 'react'
import { useAtom, useAtomValue } from 'jotai'
import { mainAtom, tokenAtom, urlAtom } from '../../atoms/atoms'

function Header (){
    let role= 'None'
    const url =useAtomValue(urlAtom)
    const [token,setToken] = useAtom(tokenAtom)
    const [_,setMain] = useAtom(mainAtom)
    if (token)
    {
        const payload = jwtDecode<MyJwt>(token)
        role = payload.role
    }
    else
    {
        role= 'None'
    }

    const HandleNavigation = (event:MouseEvent,value:string)=>{
        event.preventDefault()
        setMain(value)
    }

    const HandleDeconnection = (event:MouseEvent) =>{
        event.preventDefault()
        fetch(url+"/users/logout",{
            method:'POST',
            headers:{
                'Content-Type': 'application/json',
                'accept': '*/*'
            },
            credentials: 'include',
        }).then(response=>{
            if(!response.ok)
                throw response
            return response.json()
        }).then(data=>{
            console.log(data)
            setToken('')
            setMain('Accueil')
        })
    }


    return<>
        <nav>
            <div className='chess-menu'>
                <button onClick={ (e)=> HandleNavigation(e,'Accueil')}>Accueil</button>
                <button onClick={ (e)=> HandleNavigation(e,'Tournois')}>Tournois</button>
                {role == 'admin' && <button onClick={ (e)=> HandleNavigation(e,'Rondes')}>Rondes</button>}
                
            </div>

            <div>{role}</div>
            
            <div className='user-menu'>
                { role =='None' ?
                <>
                    <button onClick={ (e)=> HandleNavigation(e,'Connection')}>Connection</button>
                    <button onClick={ (e)=> HandleNavigation(e,'Inscription')}>Inscription</button>
                </>
                :
                <>
                    <button onClick={(e)=> HandleDeconnection(e)} >Deconnection</button>
                </>
                }
            </div>
        </nav>
    </>
}
export default Header