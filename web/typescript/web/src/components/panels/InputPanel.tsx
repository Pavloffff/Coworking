import React, { useState } from 'react'
import { Input } from 'antd'
import { FileTextOutlined, SendOutlined } from '@ant-design/icons'
import ButtonCollection from '../collections/ButtonCollection'
import BlueButton from '../buttons/BlueButton'

const InputPanel: React.FC = () => {
	const [inputValue, setInputValue] = useState<string>('')

	const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
		const value = event.target.value
		setInputValue(value)
	}

	const handleSendClick = () => {
		if (inputValue.trim() !== '') {
			console.log('Отправлен текст:', inputValue)
		} else {
			console.warn('Поле ввода пустое')
		}
	}

	return (
		<div
			style={{
				display: 'flex',
				alignItems: 'center',
				gap: '16px',
			}}
		>
			<Input
				style={{
					height: '58px',
					fontSize: '30px',
					flex: 1,
				}}
				placeholder="Печатать..."
				value={inputValue}
				onChange={handleInputChange}
			/>

			<ButtonCollection
				buttons={[
					<BlueButton
						key="button1"
						icon={<SendOutlined />}
						onClick={handleSendClick}
					/>,
					<BlueButton key="button2" icon={<FileTextOutlined />} />,
				]}
				align="14px"
			/>
		</div>
	)
}

export default InputPanel
