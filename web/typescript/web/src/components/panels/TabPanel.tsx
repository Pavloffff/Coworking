import { useState } from 'react'
import GreyButton from '../buttons/GreyButton'
import ButtonCollection from '../collections/ButtonCollection'
import {
	MenuOutlined,
	OrderedListOutlined,
	TeamOutlined,
	UserOutlined,
} from '@ant-design/icons'

const TabPanel = () => {
	const [selectedButton, setSelectedButton] = useState('btn1')

	const handleButtonClick = (buttonKey: string) => {
		setSelectedButton(buttonKey)
		console.log(`Выбрана кнопка: ${buttonKey}`)
	}

	return (
		<div
			style={{
				display: 'flex',
				alignItems: 'center',
				justifyContent: 'space-between',
				width: '100%',
			}}
		>
			<ButtonCollection
				buttons={[
					<GreyButton
						key="btn1"
						icon={<OrderedListOutlined />}
						shade={selectedButton === 'btn1' ? '#444' : '#ccc'}
						onClick={() => handleButtonClick('btn1')}
					/>,
					<GreyButton
						key="btn2"
						icon={<MenuOutlined />}
						shade={selectedButton === 'btn2' ? '#444' : '#ccc'}
						onClick={() => handleButtonClick('btn2')}
					/>,
					<GreyButton
						key="btn3"
						icon={<TeamOutlined />}
						shade={selectedButton === 'btn3' ? '#444' : '#ccc'}
						onClick={() => handleButtonClick('btn3')}
					/>,
				]}
				align="16px"
			/>

			<GreyButton
				key="rightBtn"
				icon={<UserOutlined />}
				shade={selectedButton === 'rightBtn' ? '#444' : '#ccc'}
				onClick={() => handleButtonClick('rightBtn')}
				style={{ marginLeft: 'auto' }}
			/>
		</div>
	)
}

export default TabPanel
