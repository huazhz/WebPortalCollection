package com.example.lumi.portalwebcollection.util;

import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;
import org.litepal.crud.DataSupport;

import com.example.lumi.portalwebcollection.model.cookie;

import java.util.ArrayList;
import java.util.List;

import okhttp3.Cookie;
import okhttp3.CookieJar;
import okhttp3.FormBody;
import okhttp3.HttpUrl;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;

/**
 * Created by lumi on 2017/11/7.
 */

public class HttpUtil {


    public static void sendOkHttpRequest(String address, okhttp3.Callback callback){
        OkHttpClient client = new OkHttpClient();
        Request request = new Request.Builder().url(address).build();
        client.newCall(request).enqueue(callback);
    }

    public static void sendOkHttpPost(String address, String json, okhttp3.Callback callback){
        OkHttpClient client = new OkHttpClient();
        MediaType JSON = MediaType.parse("application/json; charset=utf-8");
        RequestBody body = RequestBody.create(JSON, json);
        Request request = new Request.Builder().url(address).post(body).build();
        client.newCall(request).enqueue(callback);
    }

    public static void sendOkHttpSession(String address, String json, okhttp3.Callback callback) throws JSONException {
        JSONObject js = new JSONObject(json);
        final String username = js.getString("user_name");
        Log.d("login_username", username);
        OkHttpClient client = new OkHttpClient.Builder().cookieJar(new CookieJar() {
            @Override
            public void saveFromResponse(HttpUrl url, List<Cookie> cookies) {
                cookie ck = new cookie();
                ck.setUsername(username);
                ck.setValue(cookies.get(0).value());
                ck.setName(cookies.get(0).name());
                ck.setDomain(cookies.get(0).domain());
                ck.setPath(cookies.get(0).domain());

                ck.save();
            }

            @Override
            public List<Cookie> loadForRequest(HttpUrl url) {
                Log.d("taggg002", "sd");
                List<cookie> ck = DataSupport.where("username = ?", username).find(cookie.class);
                List<Cookie> list;
                list = new ArrayList<Cookie>();
                Log.d("taggg002", String.valueOf(ck.size()));
                if(ck.size() > 0){
                    cookie cook = ck.get(0);
                    Cookie.Builder builder = new Cookie.Builder();
                    Log.d("taggg22", cook.getName());
                    Log.d("taggg22", cook.getValue());
                    builder = builder.name(cook.getName());
                    builder = builder.value(cook.getValue());
                    builder = builder.domain(cook.getDomain());
                    builder = builder.domain(cook.getPath());
                    Log.d("taggg22", "1");
                    Cookie clientCookie = builder.build();
                    Log.d("taggg22", "1");
                    list.add(clientCookie);
                    Log.d("taggg22", "1");
                    return list;
                }else{
                    return list;
                }
            }
        }).build();

        MediaType JSON = MediaType.parse("application/json; charset=utf-8");
        RequestBody body = RequestBody.create(JSON, json);
        Request request = new Request.Builder().url(address).post(body).build();
        client.newCall(request).enqueue(callback);
    }
}
