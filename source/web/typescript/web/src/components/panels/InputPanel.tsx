import React, { useEffect, useState } from 'react'
import { Input } from 'antd'
import { FileTextOutlined, SendOutlined } from '@ant-design/icons'
import ButtonCollection from '../collections/ButtonCollection'
import BlueButton from '../buttons/BlueButton'
import Cookies from 'js-cookie'
import { chatItemsApi } from '../../api/chatItems/chatItemsApi'

interface InputPanelProps {
	currentUserId: number
	selectedTextChannelId: number | null
	refetchChat: () => void
}

const InputPanel: React.FC<InputPanelProps> = ({
	currentUserId,
	selectedTextChannelId,
	refetchChat,
}) => {
	const [access_token, setAccessToken] = useState<string | null>(null)
	const [refresh_token, setRefreshToken] = useState<string | null>(null)
	useEffect(() => {
		const access = localStorage.getItem('access_token')
		const refresh = localStorage.getItem('refresh_token')

		if (access && refresh) {
			Cookies.set('access_token', access, { secure: true, sameSite: 'Lax' })
			Cookies.set('refresh_token', refresh, { secure: true, sameSite: 'Lax' })
			setAccessToken(access)
			setRefreshToken(refresh)
		}
	}, [])

	const [inputValue, setInputValue] = useState<string>('')
	const [isSending, setIsSending] = useState(false)

	const handleSendMessage = async () => {
		if (!inputValue.trim() || !selectedTextChannelId || !currentUserId) return

		setIsSending(true)
		try {
			await chatItemsApi.addChatItem(
				0,
				currentUserId,
				selectedTextChannelId,
				inputValue.trim(),
				access_token!,
				refresh_token!
			)

			setInputValue('')
			refetchChat()
		} catch (error) {
			console.error('Ошибка отправки сообщения:', error)
		} finally {
			setIsSending(false)
		}
	}

	const handleInputChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
		const value = event.target.value
		setInputValue(value)
	}

	// const handleSendClick = () => {
	// 	if (inputValue.trim() !== '') {
	// 		console.log('Отправлен текст:', inputValue)
	// 	} else {
	// 		console.warn('Поле ввода пустое')
	// 	}
	// }

	return (
		<div
			style={{
				display: 'flex',
				alignItems: 'center',
				gap: '16px',
				marginLeft: '9px',
				marginRight: '12px',
			}}
		>
			<Input.TextArea
				style={{
					height: '58px',
					fontSize: '30px',
					flex: 1,
				}}
				placeholder="Печатать..."
				value={inputValue}
				onChange={handleInputChange}
				// onPressEnter={handleSendMessage}
				disabled={isSending || !selectedTextChannelId}
			/>

			<ButtonCollection
				buttons={[
					<BlueButton
						key="button1"
						icon={<SendOutlined />}
						onClick={handleSendMessage}
						disabled={isSending || !selectedTextChannelId}
					/>,
					<BlueButton key="button2" icon={<FileTextOutlined />} />,
				]}
				align="14px"
			/>
		</div>
	)
}

export default InputPanel
