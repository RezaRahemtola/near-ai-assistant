// @ts-expect-error TS7016
import { io } from "socket.io-client";

const socket = io("http://127.0.0.1:3001");
export default socket;
