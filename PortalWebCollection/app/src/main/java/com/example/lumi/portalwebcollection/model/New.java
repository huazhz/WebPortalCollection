package com.example.lumi.portalwebcollection.model;

import org.litepal.crud.DataSupport;

/**
 * Created by lumi on 2017/11/7.
 */

public class New extends DataSupport{
    private int id;
    private String title;
    private String url;
    private String imgurl;

    public String getImgurl() {
        return imgurl;
    }

    public void setImgurl(String imgurl) {
        this.imgurl = imgurl;
    }

    public int getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }

    public String getUrl() {
        return url;
    }

    public void setId(int id) {
        this.id = id;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public void setUrl(String url) {
        this.url = url;
    }
}
