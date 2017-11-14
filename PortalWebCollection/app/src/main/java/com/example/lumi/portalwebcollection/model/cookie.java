package com.example.lumi.portalwebcollection.model;

import org.litepal.crud.DataSupport;

import java.util.List;

import okhttp3.Cookie;

/**
 * Created by lumi on 2017/11/12.
 */

public class cookie extends DataSupport {
    private String username;
    private String value;
    private String name;
    private String path;

    public String getPath() {
        return path;
    }

    public void setPath(String path) {
        this.path = path;
    }

    public String getDomain() {
        return domain;
    }

    public void setDomain(String domain) {
        this.domain = domain;
    }

    private String domain;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getValue() {
        return value;
    }

    public void setValue(String sessionid) {
        this.value = sessionid;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

}
