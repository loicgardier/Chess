import './Header.css'
import { jwtDecode } from 'jwt-decode'
import type { MyJwt } from '../types/my_jwt'

function Header ({token}:{token:string}){
    let role= 'None'
    if (token)
    {
        const [_,payload_64,__] = token.split('.')
        const payload = jwtDecode<MyJwt>(payload_64)
        role = payload.role
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