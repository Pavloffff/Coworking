// import Cookies from 'js-cookie'
// import { useEffect, useState } from 'react'

// interface TextChannelItem {
// 	text_channel_id: number
// 	name: string
// 	server_id: number
// }

// interface TextChannelsListProps {
// 	data: TextChannelItem[]
// 	selectedTextChannelId?: string | null
// 	onItemClick?: (textChannelId: string) => void
// }

// const TextChannelsList = ({
// 	data,
// 	selectedTextChannelId,
// 	onItemClick,
// }: TextChannelsListProps) => {
// 	const [internalSelectedId, setInternalSelectedId] = useState<string | null>(
// 		() => Cookies.get('selected_server_id') || (data[0]?.text_channel_id ?? '')
// 	)

// 	useEffect(() => {
// 		if (selectedTextChannelId !== undefined) {
// 			setInternalSelectedId(selectedTextChannelId)
// 		}
// 	}, [selectedTextChannelId])

// 	const handleTextChannelClick = (textChannel: TextChannelItem) => {
// 		const newId =
// 			internalSelectedId === textChannel.text_channel_id
// 				? ''
// 				: textChannel.text_channel_id
// 	}
// }

// export default TextChannelsList
