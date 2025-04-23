export interface User {
	user_id?: number
	name: string
	email: string
	tag?: number
	password_hash: string
	password_salt?: string
	avatar_url?: string
}

export interface AuthResponse {
	access_token: string
	refresh_token: string
}

export interface AddUserResponse {
	method: string
	model: string
	data: User
}

export interface ServerModel {
	name: string
	owner_id: string
	server_id: string
	// avatar_url?: string
}

export interface ServerScheme {
	server_id?: number
	name: string
	owner: User
}

export interface TextChannelModel {
	text_channel_id: string
	name: string
	server_id: number
}

export interface ChatItemScheme {
	chat_item_id: string
	user_data: string
	text_channel_id: number
	text?: string
	file_url?: string
}

export interface ChatItemModel {
	chat_item_id?: number
	user_id: number
	text_channel_id: number
	text: string
	file_url?: string
}

export interface UserData {
	server_id: number
	user_data: string
}

export interface VoiceChannelModel {
	voice_channel_id: string
	name: string
	server_id: number
}

export interface VoiceItemModel {
	voice_item_id?: number
	user_id: number
	voice_channel_id: number
}

export interface VoiceItemScheme {
	voice_item_id?: number
	user_id: number
	user_data: string
	voice_channel_id: number
}
