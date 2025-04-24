import { List } from 'antd'
import Cookies from 'js-cookie'
import { useEffect, useState } from 'react'
import { VoiceItemScheme } from '../../api/types'

interface VoiceChannelItem {
	voice_channel_id: string
	name: string
	server_id: number
}

interface VoiceChannelsListProps {
	data: VoiceChannelItem[]
	selectedVoiceChannelId?: string | null
	onItemClick?: (textChannelId: string) => void
	voiceItemsByChannel: Record<string, VoiceItemScheme[]>
}

const VoiceChannelsList = ({
	data,
	selectedVoiceChannelId,
	onItemClick,
	voiceItemsByChannel,
}: VoiceChannelsListProps) => {
	const [internalSelectedId, setInternalSelectedId] = useState<string | null>(
		() =>
			Cookies.get('selected_voice_channel_id') ||
			(data[0]?.voice_channel_id ?? '')
	)

	useEffect(() => {
		if (selectedVoiceChannelId !== undefined) {
			setInternalSelectedId(selectedVoiceChannelId)
		}
	}, [selectedVoiceChannelId])

	const handleVoiceChannelClick = (textChannel: VoiceChannelItem) => {
		const newId =
			internalSelectedId === textChannel.voice_channel_id
				? ''
				: textChannel.voice_channel_id
		setInternalSelectedId(newId)
		onItemClick?.(newId)
		Cookies.set('selected_voice_channel_id', newId)
	}
	return (
		<List
			style={{
				height: '200px',
			}}
			itemLayout="horizontal"
			dataSource={data}
			renderItem={item => (
				<List.Item
					key={item.server_id}
					onClick={() => handleVoiceChannelClick(item)}
					style={{
						cursor: 'pointer',
						// padding: '12px 16px',
						// marginBottom: 12,
						borderBottom: '1px solid #f0f0f0',
						transition: 'background-color 0.2s',
					}}
				>
					<div style={{ width: '100%' }}>
						<List.Item.Meta
							title={
								<div
									style={{
										backgroundColor:
											item.voice_channel_id === internalSelectedId
												? '#f5f5f5'
												: 'white',
										padding: '12px 16px',
									}}
								>
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
								</div>
							}
						/>
						{voiceItemsByChannel[item.voice_channel_id]?.length > 0 && (
							<div
								style={{
									marginLeft: 8,
									marginTop: 2,
								}}
							>
								<List
									size="small"
									dataSource={voiceItemsByChannel[item.voice_channel_id]}
									style={{
										fontSize: '0.8em',
									}}
									split={false}
									renderItem={voiceItem => (
										<List.Item
											style={{
												padding: '8px 16px',
												// marginBottom: 8,
												backgroundColor: '#fafafa',
												// borderRadius: 4,
												display: 'flex',
												alignItems: 'center',
												borderBottom: 'none',
											}}
										>
											<div
												style={{
													display: 'flex',
													alignItems: 'center',
												}}
											>
												<div
													style={{
														width: 24,
														height: 24,
														borderRadius: '50%',
														// backgroundColor: '#rgb(0, 0, 0)',
														border: '1px solid',
														marginRight: 12,
														flexShrink: 0,
													}}
												/>

												<span
													style={{
														fontSize: '13px',
														color: '#666',
													}}
												>
													{voiceItem.user_data}
												</span>
											</div>
										</List.Item>
									)}
								/>
							</div>
						)}
					</div>
				</List.Item>
			)}
		/>
	)
}

export default VoiceChannelsList
