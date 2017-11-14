package com.example.lumi.portalwebcollection.util;

import android.text.TextUtils;
import android.util.Log;

import com.example.lumi.portalwebcollection.model.LoginResult;
import com.example.lumi.portalwebcollection.model.New;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by lumi on 2017/11/7.
 */

public class Utility {

    public static List<New> handleNewResponse(String response){
        if(!TextUtils.isEmpty(response)){
            try{
                List<New> allnews = new ArrayList<New>();
                JSONObject all = new JSONObject(response);
                JSONArray allNew = all.getJSONArray("news");
                for (int i = 0; i < allNew.length(); i++){
                    JSONObject newObject = allNew.getJSONObject(i);
                    New news = new New();
                    news.setId(0);
                    news.setTitle(newObject.getString("title"));
                    news.setUrl(newObject.getString("url"));
                    allnews.add(news);
                }
                return allnews;
            }catch(JSONException e){
                e.printStackTrace();
            }
        }
        return null;
    }

    public static LoginResult handleLoginResult(String response){
        if(!TextUtils.isEmpty(response)){
            try {
                JSONObject result = new JSONObject(response);
                LoginResult res = new LoginResult();
                res.setErrmeg(result.getString("error_msg"));
                Log.d("taggg6", result.getString("error_msg"));
                res.setRetcode(result.getInt("retcode"));
                if(res.getRetcode() == 0){
                    res.setNick_name(result.getString("nick_name"));
                }
                return res;
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
        return null;
    }

    public static int handleSignResult(String response){
        if(!TextUtils.isEmpty(response)){
            try {
                JSONObject result = new JSONObject(response);
                return result.getInt("retcode");
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
        return -1;
    }

}
