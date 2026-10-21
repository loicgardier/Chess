import { useAtom, useAtomValue } from "jotai";
import { useEffect, useState, type MouseEvent } from "react"
import {  mainAtom, tokenAtom, tournamentIdAtom, urlAtom } from "../../atoms/atoms";
import type { TournamentType } from "../../@types/TournamentType";
import { jwtDecode } from 'jwt-decode'
import type { MyJwt } from '../../@types/my_jwt'


function Tournois ( ){

    let role= 'None'

    const url = useAtomValue(urlAtom)

    const [tournaments,setTournaments] = useState(null)
    const [token] = useAtom(tokenAtom)
    const [_,setMain] = useAtom(mainAtom)
    const [__,setTournamentId] = useAtom(tournamentIdAtom)
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
        fetch(url+"/tournaments/",dict as RequestInit).then(response=>{
            if(!response.ok)
                throw response
            return response.json()
        }).then(data=>{
            console.log(data)
            setTournaments(data.map(
                (tournament : TournamentType) => {

                
                return <li key={tournament.id}>
                    <div>{tournament.nom}</div>
                    <div>{tournament.lieu}</div>
                    <div>{tournament.inscript}</div>
                    <div>{tournament.elo_min}</div>
                    <div>{tournament.elo_max}</div>
                    <ul>{tournament.categories.map(categorie=><li key={`${categorie.name} ${tournament.id}` }>{categorie.name}</li>)}</ul>
                    <div>{tournament.women_only}</div>
                    <div>{tournament.date_de_fin_inscription}</div>
                    <div>{tournament.status}</div>
                    <div>{tournament.ronde}</div>
                    <button onClick={e=>{HandleDetail(e,tournament.id)}}>detail</button>
                    {tournament.can_register && !tournament.is_registered && <button onClick={e=>{HandleRegister(e,tournament.id)}}>register</button>}
                    {tournament.is_registered && tournament.status=='enattente' && <button onClick={e=>{HandleUnregister(e,tournament.id)}}>unregister</button>}
                    {role == 'admin' && tournament.status=='enattente'  && <button onClick={e=>{HandleStart(e,tournament.id)}}>start</button>}
                    {role == 'admin' && tournament.status=='enattente'  && <button onClick={e=>{HandleDelete(e,tournament.id)}}>delete</button>}
                </li>
                }
            ))
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

    const HandleDetail = (event:MouseEvent,id_tournament:number)=>{
        event.preventDefault()
        setMain('DetailTournament')
        setTournamentId(id_tournament)
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
            load_data()
        }).catch(e=>{
            console.log(e)
        })
    }

    useEffect(()=>{
        load_data()
    },[])

    const HandleNavigation = (event:MouseEvent,value:string)=>{
        event.preventDefault()
        setMain(value)
    }

    return<>
    <h1>Tournois</h1>
        {role == 'admin' && <button onClick={ (e)=> HandleNavigation(e,'CreateTournament')}>Create tournament</button>}
        <ul>{tournaments}</ul>
    </>
}

export default Tournois