package com.example.lumi.portalwebcollection.model;

/**
 * Created by lumi on 2017/11/10.
 */

public class LoginResult {
    private int retcode;
    private String errmeg;
    private String nick_name;

    public int getRetcode() {
        return retcode;
    }

    public void setRetcode(int retcode) {
        this.retcode = retcode;
    }

    public String getErrmeg() {
        return errmeg;
    }

    public void setErrmeg(String errmeg) {
        this.errmeg = errmeg;
    }

    public String getNick_name() {
        return nick_name;
    }

    public void setNick_name(String nick_name) {
        this.nick_name = nick_name;
    }
}
