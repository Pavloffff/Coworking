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
