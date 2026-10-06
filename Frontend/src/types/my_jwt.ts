import { type JwtPayload } from "jwt-decode";

export interface MyJwt extends JwtPayload{
    "pseudo": string;
    "role": string;
}