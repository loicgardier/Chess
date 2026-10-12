import { useAtom } from "jotai";
import {  tokenAtom } from "../../atoms/atoms";
import { useEffect, useState } from "react";
import { jwtDecode } from "jwt-decode";
import type { MyJwt } from "../../types/my_jwt";
function Accueil ( ){

    const [nom,setNom] = useState('') 
    const [token] = useAtom(tokenAtom)

    useEffect(()=>{
        if(token)
        {
            const payload = jwtDecode<MyJwt>(token)
            setNom(payload.pseudo)
        }
        else
            setNom("")
        
    },[token])

    return<>
    <h1>Accueil</h1>
        <div>Bonjour {nom ?? nom}</div>
    </>
}

export default Accueil