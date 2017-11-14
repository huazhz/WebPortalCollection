package com.example.lumi.portalwebcollection;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.example.lumi.portalwebcollection.model.LoginResult;
import com.example.lumi.portalwebcollection.model.New;
import com.example.lumi.portalwebcollection.model.User;
import com.example.lumi.portalwebcollection.util.HttpUtil;
import com.example.lumi.portalwebcollection.util.Utility;

import org.json.JSONException;
import org.json.JSONObject;
import org.json.JSONStringer;

import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.Response;

public class SignInActivity extends AppCompatActivity {

    private String LoginName;
    private String LoginPwd;
    private int RetCode;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sign_in);

        final EditText signName = (EditText) findViewById(R.id.sign_in_usernane);
        final EditText signPwd = (EditText) findViewById(R.id.sign_in_password);
        Button Login = (Button) findViewById(R.id.login);

        Login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                final String name = signName.getText().toString();
                final String pwd = signPwd.getText().toString();
                Log.d("taggg6", name);
                Log.d("taggg6", pwd);
                login(name, pwd);
                if(RetCode == 403){
                    Toast.makeText(SignInActivity.this, "用户名或密码错误", Toast.LENGTH_SHORT).show();
                }
                else if(RetCode == 100){

                    Intent intent = new Intent(SignInActivity.this, MainActivity.class);
                    startActivity(intent);
                }else if (RetCode == -1){
                    Toast.makeText(SignInActivity.this, "登录失败", Toast.LENGTH_SHORT).show();
                }
            }
        });
    }

    public void login(String name, String pwd) {
        LoginName = name;
        LoginPwd = pwd;
        String address = "http://47.95.215.167/sign_in/";
        Log.d("login_username", LoginName);
        Log.d("login_password", LoginPwd);
        JSONObject json = new JSONObject();
        try {
            json.put("user_name",LoginName);
            json.put("password", LoginPwd);

            HttpUtil.sendOkHttpSession(address, json.toString(), new Callback() {
                @Override
                public void onFailure(Call call, IOException e) {
                    RetCode = -1;
                    Log.d("login_fail", "fail");
                }
                @Override
                public void onResponse(Call call, Response response) throws IOException {
                    String responseText = response.body().string();
                    LoginResult res = Utility.handleLoginResult(responseText);

                    if (res != null){
                        String errmsg = res.getErrmeg();
                        Log.d("taggg6", errmsg);
                        RetCode = res.getRetcode();
                        Log.d("taggg", String.valueOf(res.getNick_name()));
                        if(RetCode == 0){
                            Log.d("taggg", "oklogin");
                            User currentUser = new User();
                            currentUser.setNick_name(res.getNick_name());
                            currentUser.setUser_name(LoginName);
                            currentUser.setState(1);
                            currentUser.setPassword(LoginPwd);
                            currentUser.save();
                            RetCode = 100;
                        }
                    } else{
                        Log.d("taggg7", responseText);
                    }
                }
            });
        } catch (JSONException e) {
            e.printStackTrace();
            Log.d("taggg9", e.toString());
        }
    }
}
