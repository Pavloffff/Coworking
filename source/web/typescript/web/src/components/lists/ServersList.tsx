import { List, Avatar } from 'antd'
import Cookies from 'js-cookie'
import { useEffect, useState } from 'react'

interface ServerItem {
	server_id: string
	owner_id: string
	name: string
	avatar_url?: string
}

interface ServersListProps {
	data: ServerItem[]
}

const ServersList = ({ data }: ServersListProps) => {
	const [selectedServerId, setSelectedServerId] = useState<string>(() => {
		return Cookies.get('selected_server_id') || (data[0]?.server_id ?? '')
	})

	useEffect(() => {
		if (selectedServerId) {
			Cookies.set('selected_server_id', selectedServerId)
			const owner = data.find(s => s.server_id === selectedServerId)?.owner_id
			if (owner) Cookies.set('owner_id', owner)
		}
	}, [selectedServerId, data])

	const handleServerClick = (server: ServerItem) => {
		setSelectedServerId(prev =>
			prev === server.server_id ? '' : server.server_id
		)
	}

	return (
		<List
			itemLayout="horizontal"
			dataSource={data}
			renderItem={item => (
				<List.Item
					key={item.server_id}
					onClick={() => handleServerClick(item)}
					style={{
						cursor: 'pointer',
						padding: '12px 16px',
						borderBottom: '1px solid #f0f0f0',
						backgroundColor:
							item.server_id === selectedServerId ? '#f5f5f5' : 'white',
						transition: 'background-color 0.2s',
					}}
				>
					<List.Item.Meta
						avatar={
							<Avatar
								src={item.avatar_url}
								style={{
									backgroundColor: item.avatar_url ? 'transparent' : '#f0f0f0',
									border: '1px solid #e8e8e8',
								}}
							>
								{!item.avatar_url && ' '}
							</Avatar>
						}
						title={
							<span
								style={{
									fontWeight: 500,
									fontSize: '15px',
									color: '#333',
									whiteSpace: 'nowrap',
									overflow: 'hidden',
									textOverflow: 'ellipsis',
									maxWidth: 'calc(100% - 48px)',
								}}
							>
								{item.name}
							</span>
						}
					/>
				</List.Item>
			)}
		/>
	)
}

export default ServersList
