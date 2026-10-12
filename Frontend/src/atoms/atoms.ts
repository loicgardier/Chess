import { atom } from "jotai";

export const urlAtom = atom('http://localhost:8000')

const _token = atom('')

export const tokenAtom = atom(
    (get)=>get(_token),
    (get,set,token:string)=>{
        set(_token,token);
    }
)

const _main = atom('')

export const mainAtom = atom(
    (get)=>get(_main),
    (get,set,main:string)=>{
        set(_main,main)
    }
)