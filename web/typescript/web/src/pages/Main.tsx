import React from 'react'
import VoiceDevicesLogoPanel from '../components/panels/VoiceDevicesLogoPanel'
import InputPanel from '../components/panels/InputPanel'
import TabPanel from '../components/panels/TabPanel'
import ChatItem from '../components/chatItems/ChatItem'
import ProjectHeader from '../components/headers/ProjectHeader'

const Main: React.FC = () => {
	return (
		<div>
			<VoiceDevicesLogoPanel /> <br />
			<InputPanel /> <br />
			<TabPanel /> <br />
			<ChatItem name="Иван Иванов" text="Привет! Как дела?" />
			<ChatItem name="Мария Петрова" text="Привет! Пока не родила!" />
			<br />
			<ProjectHeader projectName="Dungeon" itemName="чат Пивальди" />
		</div>
	)
}

export default Main
