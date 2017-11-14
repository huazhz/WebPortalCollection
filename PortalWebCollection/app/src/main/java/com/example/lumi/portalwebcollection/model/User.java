package com.example.lumi.portalwebcollection.model;

import org.litepal.crud.DataSupport;

import java.io.Serializable;

/**
 * Created by lumi on 2017/11/10.
 */

public class User extends DataSupport implements Serializable {

    private String nick_name;
    private String user_name;
    private String password;
    private int state;

    public int getState() {
        return state;
    }

    public void setState(int state) {
        this.state = state;
    }

    public String getNick_name() {
        return nick_name;
    }

    public void setNick_name(String nick_name) {
        this.nick_name = nick_name;
    }

    public String getUser_name() {
        return user_name;
    }

    public void setUser_name(String user_name) {
        this.user_name = user_name;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }
}
