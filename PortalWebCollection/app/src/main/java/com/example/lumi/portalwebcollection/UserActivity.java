package com.example.lumi.portalwebcollection;

import com.example.lumi.portalwebcollection.model.cookie;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.example.lumi.portalwebcollection.model.User;
import com.example.lumi.portalwebcollection.util.HttpUtil;

import org.json.JSONException;
import org.json.JSONObject;
import org.litepal.crud.DataSupport;
import org.w3c.dom.Text;

import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.Response;

public class UserActivity extends AppCompatActivity {

    private User user;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_user);

        Intent intent = getIntent();
        user = (User) intent.getSerializableExtra("user");
        TextView currentUser = (TextView) findViewById(R.id.current_user);
        Button signIn = (Button) findViewById(R.id.sign_in);
        Button signUp = (Button) findViewById(R.id.sign_up);
        Button signOut = (Button) findViewById(R.id.sign_out);
        Button changeTags = (Button) findViewById(R.id.change_tags);

        if(user.getNick_name() != null){
            currentUser.setText("当前用户:"+user.getNick_name());
            signOut.setVisibility(View.VISIBLE);
            signIn.setVisibility(View.GONE);
            signUp.setVisibility(View.VISIBLE);
            changeTags.setVisibility(View.VISIBLE);
        }else{
            currentUser.setText("当前无用户登录");
            signOut.setVisibility(View.GONE);
            changeTags.setVisibility(View.GONE);
            signIn.setVisibility(View.VISIBLE);
            signUp.setVisibility(View.VISIBLE);
        }

        signIn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(UserActivity.this, SignInActivity.class);
                startActivity(intent);
            }
        });

        signOut.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    JSONObject json = new JSONObject();
                    json.put("user_name", user.getUser_name());
                    json.put("nick_name", user.getNick_name());
                    String url = "http://47.95.215.167/sign_out/";
                    HttpUtil.sendOkHttpSession(url, json.toString(), new Callback() {
                        @Override
                        public void onFailure(Call call, IOException e) {
                            runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    Toast.makeText(UserActivity.this, "退出失败", Toast.LENGTH_SHORT).show();
                                }
                            });
                        }

                        @Override
                        public void onResponse(Call call, Response response) throws IOException {
                            DataSupport.deleteAll(User.class);
                            DataSupport.deleteAll(cookie.class, "username = ?", user.getUser_name());
                            Intent intent = new Intent(UserActivity.this, MainActivity.class);
                            startActivity(intent);
                        }
                    });
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        });

        signUp.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(UserActivity.this, SignUpActivity.class);
                startActivity(intent);
            }
        });

        changeTags.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(UserActivity.this, TagChooseActivity.class);
                intent.putExtra("username", user.getUser_name());
                startActivity(intent);
            }
        });
    }
}
