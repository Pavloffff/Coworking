import React from 'react'
import ChatItem from '../chatItems/ChatItem'
interface ChatPanelProps {
	chatData: { photo?: string; name: string; text: string }[]
}

const ChatPanel: React.FC<ChatPanelProps> = ({ chatData }) => {
	return (
		<div
			style={{
				overflow: 'hidden',
				width: '100%',
				overflowY: 'auto',
				borderRadius: '8px',
				padding: '8px',
				boxSizing: 'border-box',
			}}
		>
			{chatData.map((item, index) => (
				<ChatItem
					key={index}
					photo={item.photo}
					name={item.name}
					text={item.text}
				/>
			))}
		</div>
	)
}

export default ChatPanel
