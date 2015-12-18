<?php

use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

/**
 * This class creates tables for dndi database.
 * 
 * Creates five tables for each of entity in dndi, and create a tag and a tagPost table to connect 
 * handle many to many relationship between entities and tag table
 */
class CreateDndiTables extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
    	# create tables
    	Schema::create('Event', function (Blueprint $table) {
    		$table->string('id')->unique();
    		$table->string('title');
    		$table->date('date')->nullable();
    		$table->longText('body');
    		$table->mediumText('url');
    		$table->string('category');
    	});
    	Schema::create('News', function (Blueprint $table) {
    		$table->string('id')->unique();
    		$table->string('title');
    		$table->date('date')->nullable();
    		$table->longText('body');
    		$table->mediumText('url');
    		$table->string('category');
    	});
    	Schema::create('InTheMedia', function (Blueprint $table) {
    		$table->string('id')->unique();
    		$table->string('title');
    		$table->date('date')->nullable();
    		$table->longText('body');
    		$table->mediumText('url');
    		$table->string('category');
    	});
    	Schema::create('PressRelease', function (Blueprint $table) {
    		$table->string('id')->unique();
    		$table->string('title');
    		$table->date('date')->nullable();
    		$table->longText('body');
    		$table->mediumText('url');
    		$table->string('category');
    	});
    	Schema::create('ScientificArticle', function (Blueprint $table) {
    		$table->string('id')->unique();
    		$table->string('title');
    		$table->date('date')->nullable();
    		$table->longText('body');
    		$table->mediumText('url');
    		$table->string('category');
    	});
    	Schema::create('tag', function (Blueprint $table) {
    		$table->integer('id')->unique();
    		$table->string('name');
    	});
    	Schema::create('tagPost', function (Blueprint $table) {
    		$table->integer('tag_id')->references('id')->on('tag');
    		$table->string('post_id');
    	});
    }

    /**
     * Reverse the migrations.
     *
     * Drop tables
     *
     * @return void
     */
    public function down()
    {
    	Schema::drop('Event');
    	Schema::drop('News');
    	Schema::drop('InTheMedia');
    	Schema::drop('PressRelease');
    	Schema::drop('ScientificArticle');
    	Schema::drop('tag');
    	Schema::drop('tagPost');
    }
}
