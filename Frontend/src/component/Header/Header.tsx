import './Header.css'
import { jwtDecode } from 'jwt-decode'
import type { MyJwt } from '../../types/my_jwt'
import { MyContext } from '../../utils/my_context'
import { use } from 'react'
import { type MouseEvent } from 'react'

function Header (){
    let role= 'None'
    const context= use(MyContext)
    if(!context)
    {
        throw new Error('Missing context');
    }
    const [token] = context.Token
    const [_,setMain] = context.Main
    if (token)
    {
        const payload = jwtDecode<MyJwt>(token)
        role = payload.role
    }

    const HandleNavigation = (event:MouseEvent,value:string)=>{
        event.preventDefault()
        setMain(value)
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
                    <button >Deconnection</button>
                </>
                }
            </div>
        </nav>
    </>
}
export default Header