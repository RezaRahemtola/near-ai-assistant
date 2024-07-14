import {
	MDBCard,
	MDBCardBody,
	MDBCardFooter,
	MDBCardHeader,
	MDBCol,
	MDBContainer,
	MDBIcon,
	MDBRow,
} from "mdb-react-ui-kit";
import { useEffect, useRef, useState } from "react";
import { v4 as uuidv4 } from "uuid";
import socket from "./socket";

type MessageAuthor = "user" | "ai";

type MessageGroup = {
	id: string;
	author: MessageAuthor;
	messages: { id: string; content: string }[];
};

export default function App() {
	const [inputValue, setInputValue] = useState("");
	const [messageGroups, setMessageGroups] = useState<MessageGroup[]>([]);
	const messageGroupsRef = useRef<MessageGroup[]>([]);
	messageGroupsRef.current = messageGroups;

	const addNewMessage = (author: MessageAuthor, content: string) => {
		const groups = messageGroupsRef.current;
		if (groups.length > 0) {
			const lastMessageGroup = { ...groups[groups.length - 1] };
			if (lastMessageGroup.author === author) {
				lastMessageGroup.messages.push({ content, id: uuidv4() });
				setMessageGroups((oldGroups) => [...oldGroups.slice(0, -1), lastMessageGroup]);
				return;
			}
		}
		setMessageGroups((oldMessageGroups) => [
			...oldMessageGroups,
			{ author, messages: [{ content, id: uuidv4() }], id: uuidv4() },
		]);
	};

	const onSubmitMessage = () => {
		socket.emit("message", inputValue);

		addNewMessage("user", inputValue);
		setInputValue("");
	};

	useEffect(() => {
		socket.connect();

		const onResponse = (value: string) => {
			addNewMessage("ai", value);
		};

		socket.on("response", onResponse);

		return () => {
			socket.off("response", onResponse);
			socket.disconnect();
		};
	}, []);

	return (
		<MDBContainer fluid className="py-5" style={{ backgroundColor: "#eee" }}>
			<MDBRow className="d-flex justify-content-center">
				<MDBCol md="10" lg="8" xl="6">
					<MDBCard id="chat2" style={{ borderRadius: "15px" }}>
						<MDBCardHeader className="d-flex justify-content-between align-items-center p-3">
							<h5 className="mb-0">Near AI Assistant</h5>
						</MDBCardHeader>
						<div className="ScrollbarsCustom native trackYVisible trackXVisible">
							<div className="ScrollbarsCustom-Content">
								<MDBCardBody>
									{messageGroups.map((messageGroup) => {
										if (messageGroup.author === "user") {
											return (
												<div className="d-flex flex-row justify-content-end mb-4 pt-1" key={messageGroup.id}>
													<div>
														{messageGroup.messages.map((message) => (
															<p
																className="small p-2 me-3 mb-1 text-white rounded-3 bg-primary"
																key={message.id}
																style={{ whiteSpace: "pre-line" }}
															>
																{message.content}
															</p>
														))}
													</div>
													<img
														src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava3-bg.webp"
														alt="avatar 1"
														style={{ width: "45px", height: "100%" }}
													/>
												</div>
											);
										}

										return (
											<div className="d-flex flex-row justify-content-start mb-4" key={messageGroup.id}>
												<img
													src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava4-bg.webp"
													alt="avatar 1"
													style={{ width: "45px", height: "100%" }}
												/>
												<div>
													{messageGroup.messages.map((message) => (
														<p
															className="small p-2 ms-3 mb-1 rounded-3"
															style={{ backgroundColor: "#f5f6f7", whiteSpace: "pre-line" }}
															key={message.id}
														>
															{message.content}
														</p>
													))}
												</div>
											</div>
										);
									})}
								</MDBCardBody>
							</div>
						</div>
						<MDBCardFooter className="text-muted d-flex justify-content-start align-items-center p-3">
							<img
								src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava3-bg.webp"
								alt="avatar 3"
								style={{ width: "45px", height: "100%" }}
							/>
							<input
								type="text"
								className="form-control form-control-lg"
								id="exampleFormControlInput1"
								placeholder="Type message"
								value={inputValue}
								onChange={(e) => setInputValue(e.target.value)}
								onKeyDown={(e) => {
									if (e.key === "Enter") {
										onSubmitMessage();
									}
								}}
							></input>
							<a className="ms-3" href="#!" onClick={() => onSubmitMessage()}>
								<MDBIcon fas icon="paper-plane" />
							</a>
						</MDBCardFooter>
					</MDBCard>
				</MDBCol>
			</MDBRow>
		</MDBContainer>
	);
}
