import { useState, useEffect } from 'react'
import TabPanel from './TabPanel'
import ServersList from '../lists/ServersList'
import { ServerModel } from '../../api/types'
import { Button, Input, Typography } from 'antd'
import { serversApi } from '../../api/servers/serversApi'
import Cookies from 'js-cookie'

interface ItemsPanelProps {
	servers?: ServerModel[] | undefined
	onServerSelect: (serverId: string) => void
	selectedServerId: string | null
}

const ItemsPanel = ({
	servers,
	onServerSelect,
	selectedServerId,
}: ItemsPanelProps) => {
	const access_token = Cookies.get('access_token') as string
	const refresh_token = Cookies.get('refresh_token') as string
	const [selectedButton, setSelectedButton] = useState('btn1')
	const [dimensions, setDimensions] = useState({
		width: window.innerWidth,
		height: window.innerHeight,
	})

	const [serverName, setServerName] = useState('')
	const handleAddServerClick = async () => {
		console.log('Введенное название сервера:', serverName)
		await serversApi.addServer(serverName, access_token, refresh_token)
		setServerName('')
	}

	useEffect(() => {
		const handleResize = () => {
			setDimensions({
				width: window.innerWidth,
				height: window.innerHeight,
			})
		}
		window.addEventListener('resize', handleResize)
		return () => window.removeEventListener('resize', handleResize)
	}, [])
	const containerWidth = Math.min(dimensions.width - 32, 460)
	const containerHeight = (dimensions.height - 32) * 0.9

	return (
		<div
			style={{
				display: 'flex',
				flexDirection: 'column',
				justifyContent: 'space-between',
				padding: '16px',
				boxSizing: 'border-box',
				width: containerWidth,
				height: containerHeight,
				border: '1px solid #e0e0e0',
				borderRadius: '8px',
				backgroundColor: '#f9f9f9',
				overflow: 'hidden',
			}}
		>
			<div
				style={{
					fontSize: '18px',
					fontWeight: 'bold',
					color: '#444',
					flexGrow: 1,
					overflowY: 'auto',
				}}
			>
				{selectedButton == 'btn1' ? (
					<div
						style={{ display: 'flex', flexDirection: 'column', height: '100%' }}
					>
						<Typography.Title
							level={3}
							style={{ marginLeft: 10, marginBottom: 16 }}
						>
							Список серверов
						</Typography.Title>

						<div style={{ flex: 1, overflowY: 'auto' }}>
							<ServersList
								data={servers || []}
								selectedServerId={selectedServerId}
								onItemClick={onServerSelect}
							/>
						</div>
						<div
							style={{
								display: 'flex',
								gap: 8,
								marginBottom: 40,
								alignItems: 'center',
							}}
						>
							<Input
								placeholder="Создать сервер"
								style={{ flex: 1 }}
								size="large"
								value={serverName}
								onChange={e => setServerName(e.target.value)}
								onPressEnter={handleAddServerClick}
							/>
							<Button
								type="primary"
								style={{
									width: 40,
									height: 40,
									flexShrink: 0,
									fontSize: '18px',
									display: 'flex',
									alignItems: 'center',
									justifyContent: 'center',
								}}
								onClick={handleAddServerClick}
							>
								+
							</Button>
						</div>
					</div>
				) : selectedButton == 'btn2' ? (
					<div
						style={{ display: 'flex', flexDirection: 'column', height: '100%' }}
					>
						<Typography.Title
							level={4}
							style={{ marginLeft: 10, marginBottom: 16 }}
						>
							Текстовые каналы
						</Typography.Title>
						<div>{selectedServerId || -1}</div>
						<div
							style={{
								display: 'flex',
								gap: 8,
								marginBottom: 40,
								alignItems: 'center',
							}}
						>
							<Input
								placeholder="Создать текстовый канал"
								style={{ flex: 1 }}
								size="large"
								value={serverName}
								onChange={e => setServerName(e.target.value)}
								onPressEnter={handleAddServerClick}
							/>
							<Button
								type="primary"
								style={{
									width: 40,
									height: 40,
									flexShrink: 0,
									fontSize: '18px',
									display: 'flex',
									alignItems: 'center',
									justifyContent: 'center',
								}}
								onClick={handleAddServerClick}
							>
								+
							</Button>
						</div>
						<Typography.Title
							level={4}
							style={{ marginLeft: 10, marginBottom: 16 }}
						>
							Голосовые каналы
						</Typography.Title>
						<div>{selectedServerId || -1}</div>
						<div
							style={{
								display: 'flex',
								gap: 8,
								marginBottom: 40,
								alignItems: 'center',
							}}
						>
							<Input
								placeholder="Создать голосовой канал"
								style={{ flex: 1 }}
								size="large"
								value={serverName}
								onChange={e => setServerName(e.target.value)}
								onPressEnter={handleAddServerClick}
							/>
							<Button
								type="primary"
								style={{
									width: 40,
									height: 40,
									flexShrink: 0,
									fontSize: '18px',
									display: 'flex',
									alignItems: 'center',
									justifyContent: 'center',
								}}
								onClick={handleAddServerClick}
							>
								+
							</Button>
						</div>
					</div>
				) : (
					<Typography.Title
						level={4}
						style={{ marginLeft: 10, marginBottom: 16 }}
					>
						Участники сервера
					</Typography.Title>
				)}
			</div>
			<div style={{ width: '100%' }}>
				<TabPanel
					selectedButton={selectedButton}
					onButtonSelect={setSelectedButton}
				/>
			</div>
		</div>
	)
}

export default ItemsPanel
