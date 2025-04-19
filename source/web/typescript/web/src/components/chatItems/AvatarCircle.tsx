import React from 'react'

interface AvatarCircleProps {
	src?: string
	size?: number
}

const AvatarCircle: React.FC<AvatarCircleProps> = ({ src, size = 64 }) => {
	return (
		<div
			style={{
				width: `${size}px`,
				height: `${size}px`,
				borderRadius: '50%',
				overflow: 'hidden',
				border: '2px solid #ccc',
				display: 'flex',
				alignItems: 'center',
				justifyContent: 'center',
				backgroundColor: '#f0f0f0',
			}}
		>
			{
				<img
					src={
						src
							? src
							: 'https://xmple.com/wallpaper/gradient-linear-white-grey-2688x1242-c2-d3d3d3-ffffff-a-15-f-14.svg'
					}
					alt=""
					style={{
						width: '100%',
						height: '100%',
						objectFit: 'cover',
					}}
				/>
			}
		</div>
	)
}

export default AvatarCircle
