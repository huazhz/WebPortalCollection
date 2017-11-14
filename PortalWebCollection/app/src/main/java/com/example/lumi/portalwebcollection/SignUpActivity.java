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
import com.example.lumi.portalwebcollection.model.User;
import com.example.lumi.portalwebcollection.util.HttpUtil;
import com.example.lumi.portalwebcollection.util.Utility;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.Response;

public class SignUpActivity extends AppCompatActivity {

    private String username;
    private String nickname;
    private String pwd1;
    private String pwd2;
    private EditText signUpUsername;
    private EditText signUpNickname;
    private EditText signUpPwd1;
    private EditText signUpPwd2;
    private int retcode;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sign_up);

        signUpUsername =  (EditText) findViewById(R.id.sign_up_username);
        signUpNickname = (EditText) findViewById(R.id.sign_up_nickname);
        signUpPwd1 = (EditText) findViewById(R.id.sign_up_pwd1);
        signUpPwd2 = (EditText) findViewById(R.id.sign_up_pwd2);
        Button signUpButton = (Button) findViewById(R.id.sign_up_button);

        signUpButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                SignUp();
                if (retcode != -1){
                    if(retcode == 10001){
                        Toast.makeText(SignUpActivity.this, "用户名已存在", Toast.LENGTH_SHORT).show();
                    }
                    else if(retcode == 0){
                        Log.d("taggg", "ok");
                        SignInActivity Login = new SignInActivity();
                        Login.login(username, pwd1);
                        Log.d("tagggg4", "123");

                        Intent intent = new Intent(SignUpActivity.this, TagChooseActivity.class);
                        intent.putExtra("username", username);
                        startActivity(intent);
                    }
                } else{
                    Toast.makeText(SignUpActivity.this, "注册失败", Toast.LENGTH_SHORT).show();
                }
            }
        });
    }

    private void SignUp() {
        username = signUpUsername.getText().toString();
        nickname = signUpNickname.getText().toString();
        pwd1 = signUpPwd1.getText().toString();
        pwd2 = signUpPwd2.getText().toString();
        if(pwd1.equals(pwd2)){
            try {
                String url = "http://47.95.215.167/sign_up/";
                JSONObject json = new JSONObject();
                json.put("nick_name", nickname);
                json.put("user_name", username);
                json.put("password", pwd1);
                Log.d("taggg", json.toString());
                HttpUtil.sendOkHttpPost(url, json.toString(), new Callback() {
                    @Override
                    public void onFailure(Call call, IOException e) {
                        retcode = -1;
                    }

                    @Override
                    public void onResponse(Call call, Response response) throws IOException {
                        String responseText = response.body().string();
                        retcode = Utility.handleSignResult(responseText);
                        Log.d("taggg", String.valueOf(retcode));
                        Log.d("taggg", String.valueOf(retcode));

                    }
                });
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }else{
            Toast.makeText(SignUpActivity.this, "密码不一致", Toast.LENGTH_SHORT).show();
        }
    }
}
