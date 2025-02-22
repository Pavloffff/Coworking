import React from 'react'
import AvatarCircle from './AvatarCircle'
import { Typography } from 'antd'

interface ChatItemProps {
	photo?: string
	name: string
	text: string
}
const { Title, Paragraph } = Typography

const ChatItem: React.FC<ChatItemProps> = ({ photo, name, text }) => {
	return (
		<div
			style={{
				display: 'flex',
				alignItems: 'flex-start',
				padding: '12px',
				border: '1px solid #e0e0e0',
				borderRadius: '8px',
				backgroundColor: '#f9f9f9',
				marginBottom: '16px',
			}}
		>
			<AvatarCircle src={photo} size={48} />

			<div
				style={{
					marginLeft: '12px',
				}}
			>
				<div
					style={{
						fontWeight: 'bold',
						fontSize: '14px',
						color: '#333',
						marginBottom: '4px',
					}}
				>
					<Title level={3} style={{ margin: 0 }}>
						{name}
					</Title>
				</div>
				<div
					style={{
						fontSize: '14px',
						color: '#555',
					}}
				>
					<Paragraph> {text} </Paragraph>
				</div>
			</div>
		</div>
	)
}

export default ChatItem
