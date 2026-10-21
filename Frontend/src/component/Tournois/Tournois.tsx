import { useAtom, useAtomValue } from "jotai";
import { useEffect, useState, type Dispatch, type MouseEvent } from "react"
import { mainAtom, tokenAtom, urlAtom } from "../../atoms/atoms";
import type { TournamentType } from "../../@types/TournamentType";



function Tournois ( ){

    const url = useAtomValue(urlAtom)

    const [tournaments,setTournaments] = useState(null)
    const [token] = useAtom(tokenAtom)

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
                    {tournament.can_register && !tournament.is_registered && <button onClick={e=>{HandleRegister(e,tournament.id)}}>register</button>}
                    {tournament.is_registered && tournament.status=='enattente' && <button onClick={e=>{HandleUnregister(e,tournament.id)}}>unregister</button>}
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

    useEffect(()=>{
        load_data()
    },[])

    return<>
    <h1>Tournois</h1>
        <ul>{tournaments}</ul>
    </>
}

export default Tournois