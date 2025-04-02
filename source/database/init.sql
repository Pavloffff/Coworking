DROP SCHEMA public;

CREATE SCHEMA public AUTHORIZATION postgres;
-- public."user" определение

-- Drop table

-- DROP TABLE public."user";

CREATE TABLE public."user" (
	user_id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
	avatar_url varchar NOT NULL,
	"name" varchar NOT NULL,
	tag int8 NOT NULL,
	password_hash varchar NOT NULL,
	password_salt varchar NOT NULL,
	CONSTRAINT user_pk PRIMARY KEY (user_id),
	CONSTRAINT user_unique UNIQUE (tag)
);


-- public."server" определение

-- Drop table

-- DROP TABLE public."server";

CREATE TABLE public."server" (
	server_id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
	"name" varchar NOT NULL,
	owner_id int8 NOT NULL,
	CONSTRAINT server_pk PRIMARY KEY (server_id)
);


-- public."right" определение

-- Drop table

-- DROP TABLE public."right";

CREATE TABLE public."right" (
	right_id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
	"name" varchar NOT NULL,
	CONSTRAINT right_pk PRIMARY KEY (right_id)
);


-- public.activitytype определение

-- Drop table

-- DROP TABLE public.activitytype;

CREATE TABLE public.activitytype (
	activity_type_id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
	"name" varchar NOT NULL,
	CONSTRAINT activitytype_pk PRIMARY KEY (activity_type_id)
);


-- public.textchannel определение

-- Drop table

-- DROP TABLE public.textchannel;

CREATE TABLE public.textchannel (
	text_channel_id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
	"name" varchar NOT NULL,
	server_id int8 NOT NULL,
	CONSTRAINT textchannel_pk PRIMARY KEY (text_channel_id),
	CONSTRAINT textchannel_server_fk FOREIGN KEY (server_id) REFERENCES public."server"(server_id) ON DELETE CASCADE ON UPDATE CASCADE
);


-- public.chatitem определение

-- Drop table

-- DROP TABLE public.chatitem;

CREATE TABLE public.chatitem (
	chat_item_id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
	user_id int8 NOT NULL,
	text_channel_id int8 NOT NULL,
	"text" varchar NULL,
	file_url varchar NULL,
	CONSTRAINT chatitem_pk PRIMARY KEY (chat_item_id),
	CONSTRAINT chatitem_textchannel_fk FOREIGN KEY (text_channel_id) REFERENCES public.textchannel(text_channel_id) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT chatitem_user_fk FOREIGN KEY (user_id) REFERENCES public."user"(user_id) ON DELETE CASCADE ON UPDATE CASCADE
);


-- public."role" определение

-- Drop table

-- DROP TABLE public."role";

CREATE TABLE public."role" (
	role_id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
	server_id int8 NOT NULL,
	"name" varchar NOT NULL,
	CONSTRAINT role_pk PRIMARY KEY (role_id),
	CONSTRAINT role_server_fk FOREIGN KEY (server_id) REFERENCES public."server"(server_id) ON DELETE CASCADE ON UPDATE CASCADE
);


-- public.roleright определение

-- Drop table

-- DROP TABLE public.roleright;

CREATE TABLE public.roleright (
	role_right_id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
	role_id int8 NOT NULL,
	right_id int8 NOT NULL,
	CONSTRAINT roleright_pk PRIMARY KEY (role_right_id),
	CONSTRAINT roleright_right_fk FOREIGN KEY (right_id) REFERENCES public."right"(right_id) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT roleright_role_fk FOREIGN KEY (role_id) REFERENCES public."role"(role_id) ON DELETE CASCADE ON UPDATE CASCADE
);


-- public.userrole определение

-- Drop table

-- DROP TABLE public.userrole;

CREATE TABLE public.userrole (
	user_role_id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
	user_id int8 NOT NULL,
	role_id int8 NOT NULL,
	CONSTRAINT userrole_pk PRIMARY KEY (user_role_id),
	CONSTRAINT userrole_role_fk FOREIGN KEY (role_id) REFERENCES public."role"(role_id) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT userrole_user_fk FOREIGN KEY (user_id) REFERENCES public."user"(user_id) ON DELETE CASCADE ON UPDATE CASCADE
);


-- public.voicechannel определение

-- Drop table

-- DROP TABLE public.voicechannel;

CREATE TABLE public.voicechannel (
	voice_channel_id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
	"name" varchar NOT NULL,
	server_id int8 NOT NULL,
	CONSTRAINT voicechannel_pk PRIMARY KEY (voice_channel_id),
	CONSTRAINT voicechannel_server_fk FOREIGN KEY (server_id) REFERENCES public."server"(server_id) ON DELETE CASCADE ON UPDATE CASCADE
);


-- public.activitychannel определение

-- Drop table

-- DROP TABLE public.activitychannel;

CREATE TABLE public.activitychannel (
	activity_channel_id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
	"name" varchar NOT NULL,
	activity_type_id int8 NOT NULL,
	server_id int8 NOT NULL,
	CONSTRAINT activitychannel_pk PRIMARY KEY (activity_channel_id),
	CONSTRAINT activitychannel_activitytype_fk FOREIGN KEY (activity_type_id) REFERENCES public.activitytype(activity_type_id) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT activitychannel_server_fk FOREIGN KEY (server_id) REFERENCES public."server"(server_id) ON DELETE CASCADE ON UPDATE CASCADE
);
