CREATE TABLE IF NOT EXISTS public.account
(
    user_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    email character varying(320) COLLATE pg_catalog."default" NOT NULL,
    name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    location character varying(40) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT account_pkey PRIMARY KEY (user_id),
    CONSTRAINT email_unique UNIQUE (email)
);


CREATE TABLE IF NOT EXISTS public.post
(
    post_id integer NOT NULL GENERATED ALWAYS AS IDENTITY (INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1),
    fk_user_id integer NOT NULL,
    post_title character varying(20) COLLATE pg_catalog."default" NOT NULL,
    post_content character varying(256) COLLATE pg_catalog."default" NOT NULL,
    location character varying(40) COLLATE pg_catalog."default" NOT NULL,
    images text[] COLLATE pg_catalog."default" NOT NULL,
    
    post_date date NOT NULL,
    CONSTRAINT post_pkey PRIMARY KEY (post_id),
    CONSTRAINT post_id UNIQUE (post_id),
    CONSTRAINT fk_user_id FOREIGN KEY (fk_user_id)
        REFERENCES public.account (user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);
ALTER TABLE public.post
ADD COLUMN tags text[] COLLATE pg_catalog."default" NOT NULL DEFAULT '{}';


CREATE TABLE IF NOT EXISTS public.saved_destination
(
    fk_folder_id integer NOT NULL,
    fk_post_id integer NOT NULL,
    CONSTRAINT saved_destination_pkey PRIMARY KEY (fk_folder_id, fk_post_id),
    CONSTRAINT fk_folder_id FOREIGN KEY (fk_folder_id)
        REFERENCES public.destination_folder (folder_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT fk_post_id FOREIGN KEY (fk_post_id)
        REFERENCES public.post (post_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);


CREATE TABLE IF NOT EXISTS public.comment
(
    comment_id integer NOT NULL GENERATED ALWAYS AS IDENTITY (INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1),
    fk_user_id integer NOT NULL,
    fk_post_id integer NOT NULL,
    comment_content character varying(100) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT comment_pkey PRIMARY KEY (comment_id),
    CONSTRAINT comment_id UNIQUE (comment_id),
    CONSTRAINT comment_fk_user_id_fkey FOREIGN KEY (fk_user_id)
        REFERENCES public.account (user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT fk_post_id FOREIGN KEY (fk_post_id)
        REFERENCES public.post (post_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

CREATE TABLE IF NOT EXISTS public.destination_folder
(
    folder_id integer NOT NULL GENERATED ALWAYS AS IDENTITY (INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1),
    fk_user_id integer NOT NULL,
    folder_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    location character varying(255) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT destination_folder_pkey PRIMARY KEY (folder_id),
    CONSTRAINT folder_id UNIQUE (folder_id),
    CONSTRAINT fk_user_id FOREIGN KEY (fk_user_id)
        REFERENCES public.account (user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);


CREATE TABLE IF NOT EXISTS public.to_do_list
(
    list_id INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY (INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1),
    fk_user_id INTEGER NOT NULL,
    to_do_name CHARACTER VARYING(20) COLLATE pg_catalog."default" NOT NULL,
    description CHARACTER VARYING(100) COLLATE pg_catalog."default",
    due_date DATE,
    status BOOLEAN NOT NULL DEFAULT FALSE,
    fk_folder_id INTEGER, -- Add the foreign key for destination folder
    CONSTRAINT to_do_list_pkey PRIMARY KEY (list_id),
    CONSTRAINT fk_user_id
        FOREIGN KEY (fk_user_id)
        REFERENCES public.account (user_id)
        MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT fk_folder_id
        FOREIGN KEY (fk_folder_id)
        REFERENCES public.destination_folder (folder_id)
        MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);
