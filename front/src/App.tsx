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
import { useEffect, useState } from "react";
import socket from "./socket";

type MessageAuthor = "user" | "ai";

type MessageGroup = {
	author: MessageAuthor;
	values: string[];
};

export default function App() {
	const [inputValue, setInputValue] = useState("");
	const [messageGroups, setMessageGroups] = useState<MessageGroup[]>([]);

	const addNewMessage = (author: MessageAuthor, content: string) => {
		console.log(messageGroups);
		if (messageGroups.length > 0) {
			const lastMessageGroup = messageGroups[messageGroups.length - 1];
			console.log(lastMessageGroup);
			if (lastMessageGroup.author === author) {
				console.log("same group");
				lastMessageGroup.values.push(content);
				setMessageGroups(messageGroups);
				return;
			}
		}
		setMessageGroups((oldMessageGroups) => [...oldMessageGroups, { author, values: [content] }]);
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
												<div className="d-flex flex-row justify-content-end mb-4 pt-1">
													<div>
														{messageGroup.values.map((message) => (
															<p className="small p-2 me-3 mb-1 text-white rounded-3 bg-primary">{message}</p>
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
											<div className="d-flex flex-row justify-content-start mb-4">
												<img
													src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava4-bg.webp"
													alt="avatar 1"
													style={{ width: "45px", height: "100%" }}
												/>
												<div>
													{messageGroup.values.map((message) => (
														<p className="small p-2 ms-3 mb-1 rounded-3" style={{ backgroundColor: "#f5f6f7" }}>
															{message}
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
