import React, { useState } from 'react'
import { Typography } from 'antd'
import {
	AudioMutedOutlined,
	AudioOutlined,
	CloseOutlined,
	CustomerServiceOutlined,
} from '@ant-design/icons'
import ButtonCollection from '../collections/ButtonCollection'
import BlueButton from '../buttons/BlueButton'

const { Title } = Typography

const toggleMicrophone = async (isOn: boolean) => {
	try {
		if (isOn) {
			const tracks = await navigator.mediaDevices.getUserMedia({ audio: true })
			tracks.getAudioTracks().forEach(track => track.stop())
			console.log('Микрофон выключен')
		} else {
			await navigator.mediaDevices.getUserMedia({ audio: true })
			console.log('Микрофон включен')
		}
	} catch (error) {
		console.error('Ошибка при работе с микрофоном:', error)
	}
}

const toggleHeadphones = (isOn: boolean) => {
	if (isOn) {
		console.log('Наушники подключены')
	} else {
		console.log('Наушники отключены')
	}
}

const VoiceDevicesLogoPanel: React.FC = () => {
	const [isMicrophoneOn, setIsMicrophoneOn] = useState(false)
	const [isHeadphonesOn, setIsHeadphonesOn] = useState(false)

	const handleMicrophoneToggle = () => {
		const newState = !isMicrophoneOn
		setIsMicrophoneOn(newState)
		toggleMicrophone(newState)
	}

	const handleHeadphonesToggle = () => {
		const newState = !isHeadphonesOn
		setIsHeadphonesOn(newState)
		toggleHeadphones(newState)
	}

	return (
		<div
			style={{
				display: 'flex',
				alignItems: 'center',
				justifyContent: 'space-between',
				gap: '16px',
			}}
		>
			<Title style={{ margin: 0 }}>КОВОРКИНГ</Title>

			<ButtonCollection
				buttons={[
					<BlueButton
						key="microphone"
						icon={isMicrophoneOn ? <AudioMutedOutlined /> : <AudioOutlined />}
						onClick={handleMicrophoneToggle}
					/>,
					<BlueButton
						key="headphones"
						icon={
							isHeadphonesOn ? <CloseOutlined /> : <CustomerServiceOutlined />
						}
						onClick={handleHeadphonesToggle}
					/>,
				]}
				align="14px"
			/>
		</div>
	)
}

export default VoiceDevicesLogoPanel
