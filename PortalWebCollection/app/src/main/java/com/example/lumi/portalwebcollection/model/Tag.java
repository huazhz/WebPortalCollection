package com.example.lumi.portalwebcollection.model;

/**
 * Created by lumi on 2017/11/13.
 */

public class Tag {
    private String kind;
    private String address;

    public Tag(String kind, String address) {
        this.kind = kind;
        this.address = address;
    }

    public String getKind() {
        return kind;
    }

    public void setKind(String kind) {
        this.kind = kind;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }
}
