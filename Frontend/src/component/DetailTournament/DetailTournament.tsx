import { useAtom, useAtomValue } from "jotai";
import { useEffect, useState, type MouseEvent } from "react"
import {  mainAtom, tokenAtom, tournamentIdAtom, urlAtom } from "../../atoms/atoms";
import { jwtDecode } from 'jwt-decode'
import type { MyJwt } from '../../@types/my_jwt'
import type { TournamentDetailType } from "../../@types/TournamentDetailType";


function DetailTournament (){

    let role= 'None'

    const url = useAtomValue(urlAtom)

    const [tournament,setTournament] = useState<TournamentDetailType>()
    const [token] = useAtom(tokenAtom)
    const [tournamentId] = useAtom(tournamentIdAtom)
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

    function load_data() {
        let dict;
        if (token)
            dict = {
                method:'GET',
                headers:{
                    'accept': '*/*',
                    'Authorization':  `Bearer ${token}` 
                },            
                credentials: 'include',
            }
        else
            dict = {
                method:'GET',
                headers:{
                    'accept': '*/*',
                },            
                credentials: 'include'
            }
        fetch(url+`/tournaments/${tournamentId}`,dict as RequestInit).then(response=>{
            if(!response.ok)
                throw response
            return response.json()
        }).then(data=>{
            console.log(data)
            setTournament(data)
        }).catch(e=>{
            console.log(e)
        })
    }


    const HandleRegister = (event:MouseEvent,id_tournament:number)=>{
        event.preventDefault()
        fetch(url+`/tournaments/${id_tournament}/register`,{
                method:'POST',
                headers:{
                    'accept': '*/*',
                    'Authorization':  `Bearer ${token}` 
                },         
                credentials: 'include',
            }).then(response=>{
            if(!response.ok)
                throw response
            load_data()
        }).catch(e=>{
            console.log(e)
        })
    }

    const HandleUnregister = (event:MouseEvent,id_tournament:number)=>{
        event.preventDefault()
        fetch(url+`/tournaments/${id_tournament}/unregister`,{
                method:'POST',
                headers:{
                    'accept': '*/*',
                    'Authorization':  `Bearer ${token}` 
                },         
                credentials: 'include',
            }).then(response=>{
            if(!response.ok)
                throw response
            load_data()
        }).catch(e=>{
            console.log(e)
        })
    }

    const HandleStart = (event:MouseEvent,id_tournament:number)=>{
        event.preventDefault()
        fetch(url+`/tournaments/${id_tournament}/start`,{
                method:'post',
                headers:{
                    'accept': '*/*',
                    'Authorization':  `Bearer ${token}` 
                },         
                credentials: 'include',
            }).then(response=>{
            if(!response.ok)
                throw response
            load_data()
        }).catch(e=>{
            console.log(e)
        })
    }
    const HandleDelete = (event:MouseEvent,id_tournament:number)=>{
        event.preventDefault()
        fetch(url+`/tournaments/${id_tournament}`,{
                method:'DELETE',
                headers:{
                    'accept': '*/*',
                    'Authorization':  `Bearer ${token}` 
                },         
                credentials: 'include',
            }).then(response=>{
            if(!response.ok)
                throw response
            setMain('Tournois')

        }).catch(e=>{
            console.log(e)
        })
    }

    useEffect(()=>{
        load_data()
    },[])


    
    return<>
    <h1>Détail tournois {tournamentId}</h1>
    <div>{tournament?.nom}</div>
    <div>{tournament?.lieu}</div>
    <div>{tournament?.inscript}</div>
    <div>{tournament?.elo_min}</div>
    <div>{tournament?.elo_max}</div>
    <ul>{tournament?.categories.map(categorie=><li key={`${categorie.name} ${tournament.id}` }>{categorie.name}</li>)}</ul>
    <div>{tournament?.women_only}</div>
    <div>{tournament?.date_de_fin_inscription}</div>
    <div>{tournament?.status}</div>
    <ul>{tournament?.inscripts.map(inscript=><li key={`${inscript} ${tournament.id}` }>{inscript}</li>)}</ul>
    <div>Ronde: {tournament?.ronde}</div>
    <ul>{tournament?.rencontres.map(rencontre=><li key={`${rencontre.id}`}>
                                                    <ul>
                                                        <li>blanc: {rencontre.blanc}</li>
                                                        <li>noir: {rencontre.noir}</li>
                                                        <li>resultat: {rencontre.result}</li>
                                                    </ul>
                                                </li>)}
    </ul>

    {tournament?.can_register && !tournament.is_registered && <button onClick={e=>{HandleRegister(e,tournament.id)}}>register</button>}
    {tournament?.is_registered && tournament.status=='enattente' && <button onClick={e=>{HandleUnregister(e,tournament.id)}}>unregister</button>}
    {role == 'admin' && tournament?.status=='enattente'  && <button onClick={e=>{HandleStart(e,tournament.id)}}>start</button>}
    {role == 'admin' && tournament?.status=='enattente'  && <button onClick={e=>{HandleDelete(e,tournament.id)}}>delete</button>}
    </>
}

export default DetailTournament