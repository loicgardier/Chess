import './Header.css'
import { jwtDecode } from 'jwt-decode'
import type { MyJwt } from '../types/my_jwt'
import { TokenContext } from '../utils/token_context'
import { use } from 'react'

function Header (){
    let role= 'None'
    const tokenContext= use(TokenContext)
    if(tokenContext)
    {
        const [token] = tokenContext
        if (token)
        {
            const payload = jwtDecode<MyJwt>(token)
            role = payload.role
        }
    }

    return<>
        <nav>
            <div className='chess-menu'>
                <a href="/">Accueil</a>
                <a href="/tournois">Tournois</a>
                {role == 'Admin' && <a href='/ronde'>Rondes</a>}
                
            </div>
            
            <div className='user-menu'>
                { role =='None' ?
                <>
                    <a href="/connection">Connection</a>
                    <a href="/inscription">Inscription</a>
                </>
                :
                <>
                    <a href='/deconnection'>Deconnection</a>
                </>
                }
            </div>
        </nav>
    </>
}
export default Header